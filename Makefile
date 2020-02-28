
upload_assets:

	echo "Compressing assets..."
	zip -r /tmp/current.zip assets/
	sha=$(git rev-parse HEAD)
	echo "Compression complete."
	echo "Relacing current assets at: s3://gltd/git/fifteenpm-assets/assets/current.zip"
	make remove_current_remote_assets
	aws --profile gltd s3 cp /tmp/current.zip s3://gltd/git/fifteenpm-assets/assets/current.zip
	rm -f /tmp/current.zip
	echo "Saving snapshot of assets..."
	aws --profile gltd s3 cp s3://gltd/git/fifteenpm-assets/assets/current.zip "s3://gltd/git/fifteenpm-assets/assets/$(git rev-parse HEAD).zip"
	echo "Done..."

download_assets:

	echo "Downloading current assets"
	aws --profile gltd s3 cp s3://gltd/git/fifteenpm-assets/assets/current.zip /tmp/current.zip
	unzip /tmp/current.zip
	mv /tmp/assets/ ./assets/
	rm -rf /tmp/current.zip /tmp/assets/

remove_current_remote_assets:
	
	aws --profile gltd s3 rm --recursive s3://gltd/git/fifteenpm-assets/assets/current.zip