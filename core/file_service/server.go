package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func main() {
	r := gin.Default()
	r.Static("/file", "./assets")
	r.Use(MyACustomMiddleware())

	// r.Use(cors.New(cors.Config{
	// 	AllowOrigins:     []string{"http://localhost:3000"},
	// 	AllowMethods:     []string{http.MethodGet, http.MethodPatch, http.MethodPost, http.MethodHead, http.MethodDelete, http.MethodOptions},
	// 	AllowHeaders:     []string{"Content-Type", "X-XSRF-TOKEN", "Accept", "X-Requested-With", "Authorization"},
	// 	ExposeHeaders:    []string{"Content-Length"},
	// 	AllowCredentials: true,
	// }))

	r.Use(CORS())
	// r.Use(cors.New())
	//upload single file
	r.MaxMultipartMemory = 8 << 20 // 8 MiB
	r.POST("/upload", func(context *gin.Context) {
		file, header, err := context.Request.FormFile("file")
		if err != nil {
			context.String(http.StatusBadRequest, fmt.Sprintf("file err : %s", err.Error()))
			return
		}

		filename := header.Filename

		log.Println(">>>>>>>>>>>>" + filename)
		newFilename := uuid.New().String() + filepath.Ext(filename)
		out, err := os.Create("./assets/" + newFilename)
		if err != nil {
			log.Fatal(err)
		}
		defer out.Close()

		_, err = io.Copy(out, file)
		if err != nil {
			log.Fatal(err)
		}
		filepath := "http://localhost:8080/file/" + newFilename
		context.JSON(http.StatusOK, gin.H{"filepath": filepath})
	})

	r.MaxMultipartMemory = 8 << 20 // 8 MiB
	r.POST("/upload_multiple_file", func(context *gin.Context) {

		form, err := context.MultipartForm()
		if err != nil {
			log.Fatal(err)
		}

		files := form.File["upload"]
		newFiles := make([]string, len(files))

		for index, file := range files {

			newFilename := uuid.New().String() + filepath.Ext(file.Filename)

			context.SaveUploadedFile(file, "./assets/"+newFilename)

			filepath := "http://localhost:8080/file/" + newFilename

			newFiles[index] = filepath
		}
		context.JSON(http.StatusOK, gin.H{
			"number-file-upload": len(files),
			"filepaths":          newFiles,
		})
	})

	r.Run(":8080")
}

func MyACustomMiddleware() gin.HandlerFunc {
	return func(context *gin.Context) {
		if true {
			context.Next()
		}
	}
}

func CORS() gin.HandlerFunc {
	return func(c *gin.Context) {
		log.Println(c.Request.Method)
		c.Writer.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
		// c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With, Bearer")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}