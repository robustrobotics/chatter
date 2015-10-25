# chatter
A simple bot to talk to github

## Installation
First, install `uwsgi` and `flask`
```bash
sudo apt-get install uwsgi uwsgi-plugin-python python-flask
```

Next, configure `nginx` by adding the following lines to a server block.

```
location /chatter/ {
  include uwsgi_params;
  uwsgi_pass 127.0.0.1:9001;
}
```


## Todo

Look at making the robot more conversational.
[NLTK](http://www.nltk.org/api/nltk.chat.html) is a good start, and
[this](http://stackoverflow.com/a/9707402/1779949) StackOverflow answer has some
more links.
