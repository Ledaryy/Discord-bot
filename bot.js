const Discord = require("discord.js")
const client = new Discord.Client()

client.on("ready", () => {
    console.log(`logged in as ${client.user.tag}!`)
})

client.on("message", msg => {
    if (msg.content == "da") {
        msg.reply("net")
    }
})

client.on("message", msg => {
    if (msg.content == "Вопрос для @Ledary  : почему каждый день не обновляем?") {
        msg.reply(":whynot4:");
        msg.reply("откуда знать")
        msg.reply("вроде и так пойдёт")
    }
})

client.login(process.env.TOKEN)