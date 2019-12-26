const TOKEN = process.env.token;
const CONFIRMATION = process.env.confirmation;
const LOGIN = process.env.login;
const PASSWORD = process.env.password;
const DNSID = process.env.DNSID;

const express = require('express')
const bodyParser = require('body-parser')
const VkBot = require('node-vk-bot-api')
 
const app = express()

const spawn = require('child_process').spawn

const bot = new VkBot({
  token: TOKEN,
  confirmation: CONFIRMATION,
})
 
bot.command('/дз', (ctx) => {
	ctx.reply("В процессе...")
	let pyProg = spawn('python', ['eduTatarParser.py', DNSID])
	pyProg.stdout.on('data', (data) => {
		let st = data.toString('utf-8');
		let result = Buffer.from(st, 'base64').toString('utf-8');
		ctx.reply(result);
	});
	pyProg.stderr.on('data', (data) => {
		ctx.reply(data.toString());
	});
	pyProg.on('error', (err) => {
		ctx.reply(err.toString());
	});

});

app.use(bodyParser.json())
 
app.post('/', bot.webhookCallback)
 
app.listen(process.env.PORT || 8000, () => console.log("Start!"))