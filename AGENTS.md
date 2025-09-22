# AGENTS.md

## Context

I want to create a discord bot in python for posting a daily thread to a forum chanel,
where users would post their results from the daily game and the discord bot
would parse their result to tally the wins.

- We want to keep track of the # of the post, configurable by a json file so
  that it can be controlled that way.
- It should post the current date of on the post

Examples of the results for the different games:

clues by sam:

```
I solved the daily Clues by Sam (Sep 21st 2025) in less than 26 minutes
🟩🟩🟨🟨
🟨🟩🟨🟩
🟩🟨🟩🟩
🟨🟨🟩🟩
🟩🟩🟨🟨
https://cluesbysam.com
```

kinda hard golf:

```
kindahard.golf 09/21

📝 15

5.⛳ -
4.⛳ 2
3.⛳ 1
2.⛳ 4
1.⛳ 3
0.🏌️ 5

https://kindahard.golf
```

angle.wtf:

```
#Angle #1188 X/4
⬆️⬆️⬆️⬆️: 1° off
https://www.angle.wtf
```
