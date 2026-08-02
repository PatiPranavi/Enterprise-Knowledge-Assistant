css = """
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.chat-message{
    padding:1.2rem;
    border-radius:12px;
    margin-bottom:1rem;
    display:flex;
}

.chat-message.user{
    background:#2b313e;
}

.chat-message.bot{
    background:#475063;
}

.chat-message .avatar{
    width:20%;
}

.chat-message .avatar img{
    max-width:60px;
    max-height:60px;
    border-radius:50%;
}

.chat-message .message{
    width:80%;
    padding:0 1rem;
    color:white;
}

</style>
"""

user_template = """
<div class="chat-message user">
<div class="avatar">
<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">
</div>

<div class="message">{{MSG}}</div>

</div>
"""

bot_template = """
<div class="chat-message bot">
<div class="avatar">
<img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
</div>

<div class="message">{{MSG}}</div>

</div>
"""