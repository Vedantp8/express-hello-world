const express = require("express")
const app = express()
const port = process.env.PORT || 3001
const jsonData = require("./jsonData/scraped_data.json")
const { exec } = require("child_process")
const fs = require("fs")
const path = require("path")

app.get("/", (req, res) => res.type("html").send(html))

app.get("/hi", (req, res) => res.send("hello world"))

app.get("/hello", (req, res) => res.send(jsonData))

app.get("/scrape-data", (req, res) => {
  try {
    console.log("process initiated")
    // Execute the Python script
    exec("python script.py", (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error.message}`)
        // return res.status(500).json({ error: "Failed to execute script" })
      }

      // Path to the generated JSON file
      const filePath = path.join(__dirname, "./jsonData/scraped_data.json")

      // Check if file exists
      fs.readFile(filePath, "utf8", (err, data) => {
        if (err) {
          console.error(`Error reading JSON file: ${err.message}`)
          // return res.status(500).json({ error: "Failed to read JSON data" })
        }

        // Send JSON data to the frontend
        res.setHeader("Content-Type", "application/json")
        res.send(data)
      })
    })
  } catch (error) {
    console.log(error)
    res.send(error)
  }
})

const server = app.listen(port, () =>
  console.log(`Example app listening on port ${port}!`)
)

server.keepAliveTimeout = 120 * 1000
server.headersTimeout = 120 * 1000

const html = "Hi"
