#/bin/sh

echo "Compressing assets..."
zip -r /tmp/current.zip assets/
echo "Compression complete."
echo "Relacing current assets at: s3://gltd/git/fifteenpm-assets/assets/current.zip"
aws --profile gltd s3 rm --recursive s3://gltd/git/fifteenpm-assets/assets/current.zip
aws --profile gltd s3 cp /tmp/current.zip s3://gltd/git/fifteenpm-assets/assets/current.zip
rm -f /tmp/current.zip
SHA=$(git rev-parse HEAD)
echo "Saving snapshot of assets for SHA: $SHA..."
aws --profile gltd s3 cp s3://gltd/git/fifteenpm-assets/assets/current.zip "s3://gltd/git/fifteenpm-assets/assets/$SHA.zip"
echo "Done."
