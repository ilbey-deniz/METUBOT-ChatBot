const express = require('express')
const fs = require('fs')

if (!fs.existsSync('.env')) {
    fs.copyFileSync('.env.example', '.env');
    console.log('Created .env file from .env.example');
}
require('dotenv').config()

var path = require('path');
var cors = require('cors')
const app = express()
const httpServer = require("http").createServer(app);
const http = require('http');
// parse json objects
app.use(express.json())

app.use(cors());

const io = require("socket.io")(httpServer, {});

io.on("connection", (socket) => {
    console.log('socket io connected.');
    socket.emit('chat answer', 'Merhaba, ben Metubot 🤖');
    socket.emit('chat answer', 'Sizlere nasıl yardımcı olabilirim?');
    socket.on('chat question', (msg) => {
        console.log('question: ' + msg);
        http.get(process.env.FLASK_URL + "/ask", params = { 'question': msg }, (res) => {
            let data = '';
            res.setEncoding('utf8');

            res.on('data', (chunk) => {
                data += chunk;
            });

            // The whole response has been received. Print out the result.
            res.on('end', () => {
                console.log('received answer:', data);
                data = data.replace(/^"(.*)"$/, '$1'); // remove string quotes
                socket.emit('chat answer', data);
            });
        }).on('error', (e) => {
            console.error(`Got error: ${e.message}. Make sure NLP API server is running.`);
        });

    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
    ;

});

const FRONTEND_FILES_LOCATION = process.env.FRONTEND_FILES_LOCATION;
app.use(express.static(path.join(__dirname, FRONTEND_FILES_LOCATION)));

app.post('/', (req, res) => {

    // console.log(req.body)
    res.send("mesaj alındı");
})

const PORT = process.env.PORT || 3000;
httpServer.listen(PORT, () => {
    console.log(`listening at http://localhost:${PORT}`);
});



