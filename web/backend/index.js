const express = require('express')
const dotenv = require('dotenv');
dotenv.config();
var path = require('path');
var cors = require('cors')
const app = express()
// parse json objects
app.use(express.json()) 


app.use(cors());

const FRONTEND_FILES_LOCATION = process.env.FRONTEND_FILES_LOCATION;
app.use(express.static(path.join(__dirname, FRONTEND_FILES_LOCATION)));

app.post('/', (req, res) => {
    console.log(req.body)
    res.send("mesaj alındı");
})

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`listening at http://localhost:${PORT}`);
});
