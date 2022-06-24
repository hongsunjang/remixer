const express = require('express');
require('dotenv').config();
const querystring = require('querystring');
const axios = require('axios');
const url = require('url');
const https = require('https')
const fs = require('fs');
const { resolveNs } = require('dns');
const { exec } = require('child_process');
const pythonshell = require('python-shell');

const app = express();
const port = 8888;
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const REDIRECT_URI = process.env.REDIRECT_URI;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/json', (req, res) => {
  const data = {
    name: 'hongsun',
    isPerson: true

  };
  res.json(data)
});

app.get('/api/login', (req, res) => {
  const queryParams = querystring.stringify({
    client_id: CLIENT_ID,
    response_type: 'code',
    redirect_uri: REDIRECT_URI,
  });
  res.redirect(`https://accounts.spotify.com/authorize?${queryParams}`)
});

app.get('/api/callback', (req, res)=>{
    const code = req.query.code || null;
    axios({
      method: 'post',
      url: 'https://accounts.spotify.com/api/token',
      data: querystring.stringify({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: REDIRECT_URI
      }),
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${new Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')}`,
      },
    })
    .then(response => {
        if (response.status === 200) {
            const { access_token, token_type} = response.data;
            const queryParams = querystring.stringify({
              access_token,
              token_type
            });
            res.redirect(`http://localhost:3000/?${queryParams}`)
        }
    })
    .catch(error => {
        res.send(error);
    });

});

app.get('/api/remix', async (req, res)=>{
  const name=req.query.name;
  const token_type = req.query.token_type;
  const access_token = req.query.access_token;
  //exec(`spleeter separate -p spleeter:2stems -o output/ ${name}`, 
  exec(`ls`, 
    (err, stdout, stderr) => {
      if (err) {
        // node couldn't execute the command
        console.log(err)
        return;
      }

      // the *entire* stdout and stderr (buffered)
      console.log(`stdout: ${stdout}`);
      console.log(`stderr: ${stderr}`);
      var options = {
        mode: 'text',
        pythonOptions: [],
        args: []
      };

      pythonshell.PythonShell.run('hello.py', options, (err, results) =>{
        if (err) console.log(err);
        else console.log(results);
      });
  });

});

app.get('/api/search', async (req, res)=>{
  const name=req.query.name;
  const token_type = req.query.token_type;
  const access_token = req.query.access_token;
  let payload = {
    q: name,
    type: 'track,artist',
    market: 'US',
    limit: '3',
    offset: '0',
  }
  const params =new url.URLSearchParams(payload);
  try{
    const response = await axios.get(`https://api.spotify.com/v1/search?${params}`,{
      headers: {
        Authorization: `${token_type} ${access_token}`
      }
    });
    const tracks =response.data.tracks.items;
    console.log(tracks.length);
    var items = []; 
    var idx;
    for(idx=0; idx< tracks.length;idx++){
      const track = tracks[idx]; 
      const id= track.id;
      const real_name = track.name;
      const preview_url = track.preview_url;
      const artist = track.artists[0].name;
      const image_url = track.album.images[0].url;
      console.log(real_name)
      if (preview_url != null){
        https.get(preview_url, resp => {
          console.log('preview url download')
          resp.pipe(fs.createWriteStream(`${real_name}.mp3`))
        })    
        console.log('download success');
      }else{
        console.log('download failed')
      }
      const response = await axios.get(`https://api.spotify.com/v1/audio-features/${id}`, {
        headers: {
          Authorization: `${token_type} ${access_token}`
        }
      });
      const info = {
        'index': idx,
        'real_name': real_name,
        'preview_url': preview_url,
        'artist': artist,
        'image_url': image_url,
      }
      items.push(info)
    } 
    console.log(items)
    //res.send(`${JSON.stringify(items, null, 2)}`);
    res.json(JSON.stringify({data:items}));
  }catch(err){
    res.send(err);
  }
});


app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
})