
upload_assets:

	sha=$(git rev-parse HEAD)
	echo "replacing current"
	make remove_current_remote_assets
	aws --profile gltd s3 sync assets/ s3://gltd/git/fifteenpm-assets/assets/current/
	echo "saving snapshot"
	sha=$(`git rev-parse HEAD`)
	aws --profile gltd s3 sync assets/ "s3://gltd/git/fifteenpm-assets/assets/$sha/"

download_assets:

	aws --profile gltd s3 sync s3://gltd/git/fifteenpm-assets/assets/current/ assets/

remove_current_remote_assets:
	
	aws --profile gltd s3 rm --recursive s3://gltd/git/fifteenpm-assets/assets/current/