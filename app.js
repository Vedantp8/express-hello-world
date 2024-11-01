const express = require("express")
const app = express()
const { exec } = require("child_process")
const fs = require("fs")
const path = require("path")
const port = 3000
const fallBackJson = require("./jsonData/scraped_data.json")
const cors = require("cors")

require("dotenv").config()

app.use(
  cors({
    origin: ["http://localhost:5173", "https://drinks-data-seven.vercel.app/"],
  })
)

const API_KEY = process.env.API_KEY

const checkApiKey = (req, res, next) => {
  const apiKey = req.headers["x-api-key"]

  if (apiKey && apiKey === API_KEY) {
    next()
  } else {
    return res.status(403).json({ error: "Forbidden: Invalid API Key" })
  }
}

app.get("/scrape-data", checkApiKey, (req, res) => {
  try {
    console.log("process initiated")

    exec("python script.py", (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error.message}`)
        return res.status(500).json({ error: "Failed to execute script" })
      }

      const filePath = path.join(__dirname, "./jsonData/scraped_data.json")

      fs.readFile(filePath, "utf8", (err, data) => {
        if (err) {
          console.error(`Error reading JSON file: ${err.message}`)
          return res.status(500).json({ error: "Failed to read JSON data" })
        }

        res.setHeader("Content-Type", "application/json")
        res.send(data)
      })
    })
  } catch (error) {
    console.log(error)
    res.status(500).json({ error: "An unexpected error occurred" })
  }
})

app.get("/fetch-data", checkApiKey, (req, res) => {
  console.log("Fetching data...")

  try {
    res.status(200).json(fallBackJson)
  } catch (error) {
    console.error("Error fetching data:", error)
    res.status(500).json(fallBackJson)
  }
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
