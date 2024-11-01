const express = require("express")
const app = express()
const port = process.env.PORT || 3001
const jsonData = require("./jsonData/scraped_data.json")
const { exec } = require("child_process")
const fs = require("fs")
const path = require("path")

app.get("/fetch-data", (req, res) => {
  console.log("Fetching data...")

  try {
    res.status(200).json(jsonData)
  } catch (error) {
    console.error("Error fetching data:", error)
    res.status(500).json(jsonData)
  }
})

app.get("/scrape-data", (req, res) => {
  try {
    console.log("process initiated")

    // Executing the Python script
    exec("python script.py", (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error.message}`)
        return res.status(500).json({ error: "Failed to execute script" })
      }

      const filePath = path.join(__dirname, "./jsonData/scraped_data.json")

      // Checking if file exists
      fs.readFile(filePath, "utf8", (err, data) => {
        if (err) {
          console.error(`Error reading JSON file: ${err.message}`)
          return res.status(500).json({ error: "Failed to read JSON data" })
        }

        // Sending the scraped data to the frontend
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
