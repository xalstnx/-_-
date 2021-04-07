import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

from apiclient.discovery import build
import argparse
DEVELOPER_KEY = "your key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


app = Flask(__name__)

@app.route('/concrawl', methods=['GET'])
def crawler():
	fid = request.args.get('fid')
	fname = str(request.args.get('fname')) + '만들기'
	baseurl = 'https://terms.naver.com/entry.nhn?docId='
	searchurl = baseurl + str(fid)
	res = requests.get(searchurl)
	parsing = BeautifulSoup(res.content, 'html.parser')
	contents = parsing.select('div.size_ct_v2')
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--q", help="Search term", default=fname)
	argparser.add_argument("--max-results", help="Max results", default=1)
	args = argparser.parse_args()
	#youtube_search(args)
	return remove_all_img(str(contents)) + str(youtube_search(args))

#모든img태그를 삭제하는 함수
def remove_all_img(content):
	for i in range(content.count('<img')):
		img_start = content.find('<img')
		img_end = content.find('>', img_start)
		content = content.replace(content[img_start:img_end+1], "")
	return content


def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	search_response = youtube.search().list(
		q=options.q,
		part="id,snippet",
		maxResults=options.max_results
	).execute()

	videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append("@#$%s@%s" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
	print(videos)
	return videos


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5001)