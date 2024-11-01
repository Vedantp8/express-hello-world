const express = require("express")
const app = express()
const port = process.env.PORT || 3001
const jsonData = require("./jsonData/scraped_data.json")

app.get("/", (req, res) => res.type("html").send(html))

app.get("/hi", (req, res) => res.send("hello world"))

app.get("/hello", (req, res) => res.send(jsonData))

const server = app.listen(port, () =>
  console.log(`Example app listening on port ${port}!`)
)

server.keepAliveTimeout = 120 * 1000
server.headersTimeout = 120 * 1000

const html = "Hi"
