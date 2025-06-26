const https = require('https');

const options = {
  hostname: '1jjdwnh7k5.execute-api.us-east-1.amazonaws.com',
  port: 443,
  path: '/Prod/resources/',
  method: 'GET'
};

const req = https.request(options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log(`BODY: ${data}`);
  });
});

req.on('error', (e) => {
  console.error(`ERROR: ${e.message}`);
});

req.end();