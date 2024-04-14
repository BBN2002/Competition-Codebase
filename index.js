const express = require('express');
const app = express();
const mysql = require('mysql');
const bodyParser = require('body-parser');
const cors = require('cors');
const https = require('https');
const fs = require('fs');

app.use(cors());
app.use(bodyParser.json());


const database = mysql.createPool({
    host: '123.57.92.58',
    port: 3306,
    user: '租房数据',
    password: 'Kingho325',
    database: '租房数据',
    charset: 'utf8',
});

app.get('/getHouses', (req, res) => {
    database.query('SELECT * FROM 在建房数据', (err, results) => {
        if (err) {
            const result = {
                warn: 'error',
                message: '获取数据库时发生错误'
            };
            res.send(JSON.stringify(result));
        } else {
            res.send(JSON.stringify(results));
        }
    });
});

app.get('/getRTHouses', (req, res) => {
    database.query('SELECT * FROM 租房数据', (err, results) => {
        if (err) {
            const result = {
                warn: 'error',
                message: '获取数据库时发生错误'
            };
            res.send(JSON.stringify(result));
        } else {
            res.send(JSON.stringify(results));
        }
    });
});

class House {
    constructor(data) {
        this.title = data.title;
        this.link = data.link;
        this.location = data.location;
        this.latitude = data.latitude;
        this.price = data.price;
        this.bedroom = data.bedroom;
        this.space = data.space;
        this.available_time = data.available_time;
    }
}

const options = {
    key: fs.readFileSync('/www/wwwroot/test/www.ksjzs.com.key'),
    cert: fs.readFileSync('/www/wwwroot/test/www.ksjzs.com.pem')
};

https.createServer(options, app).listen(8000, () => {
    console.log('HTTPS Server is running on port 8000');
});
