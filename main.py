import time
from pytube import YouTube
from flask import Flask, jsonify, request
from flask_cors import CORS
from hurry.filesize import size


app = Flask(__name__)
CORS(app)

def istekYolla(url):
    yt = YouTube(url)
    data = {
        "title": yt.title,
        "auther": yt.author,
        "description": yt.description,
        "length": time.strftime("%H:%M:%S", time.gmtime(yt.length)),
        "views": yt.views,
        "publish_date": yt.publish_date,
        "thumbnail": yt.thumbnail_url,
        "sources": []
    }
    videos = yt.streams.filter(progressive=True)
    for d in videos:
        data["sources"].append({
            "url": d.url,
            "resolution": d.resolution,
            "size": size(d.filesize)
        })
    return data

@app.route("/")
def youtubeApi():
    url = request.args.get("url")
    data = istekYolla(url=url)
    return jsonify(data)



if __name__ == "__main__":
    app.run()