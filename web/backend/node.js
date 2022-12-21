// not: exit denmediği için shell açık kalabilir node.js sona erse de.
// (belki de çocuk olduğu için otomatik olarak öldürülebilir)

const express = require('express')
const fs = require('fs')
const { exec } = require("child_process");
const {getPersistentShell, getShellProc} = require('./DangerousSSH');


// End
/* todo:
spawnedShell.stdin.end();
*/


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

const spawnedShell = getShellProc();
const io = require("socket.io")(httpServer, {});
let sshSeqNum = 0;
// Capture stdout
spawnedShell.stdout.on('data', d => {
    let out = d.toString();
    console.log('ssh out: ', out);
    io.emit('ssh out', {
        content: out,
        dateMs: Date.now(),
        sshSeqNum: sshSeqNum++
    });
});
spawnedShell.stderr.on('data', d => {
    let out = d.toString();
    console.log('ssh err: ', out);
    io.emit('ssh out', {
        content: out,
        dateMs: Date.now(),
        sshSeqNum: sshSeqNum++
    });
});
io.on("connection", (socket) => {
    console.log('socket io connected.');
    socket.emit('chat answer', 'Merhaba, ben Metubot 🤖');
    socket.emit('chat answer', 'Sizlere nasıl yardımcı olabilirim?');
    socket.on('chat question', (msg) => {
        console.log('question: ' + msg);
        http.get(process.env.FLASK_URL + `/ask?question=${msg}`, (res) => {
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
    socket.on('ssh in', (msg) => {
        console.log('ssh in: ' + msg);
        spawnedShell.stdin.write(`${msg}\n`);
        /*io.emit('ssh out', {
            content: `>${msg}`,
            dateMs: Date.now(),
            sshSeqNum: sshSeqNum++
        });*/

    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });


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





