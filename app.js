const express = require("express")
const app = express()
const { exec } = require("child_process")
const fs = require("fs")
const path = require("path")
const port = 3000
const fallBackJson = require("./jsonData/scraped_data.json")

app.get("/scrape-data", (req, res) => {
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
    res.errored(error)
  }
})

app.get("/fetch-data", (req, res) => {
  console.log("Fetching data...")

  try {
    res.status(200).json(fallBackJson)
  } catch (error) {
    console.error("Error fetching data:", error)
    res.status(500).json(fallBackJson)
  }
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
