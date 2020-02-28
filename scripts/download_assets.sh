#/bin/sh

echo "Downloading current assets..."
aws --profile gltd s3 cp s3://gltd/git/fifteenpm-assets/assets/current.zip /tmp/current.zip
echo "Syncing with local assets, you'll be able to decide how to preserve with changes/updates..."
unzip /tmp/current.zip
rm -rf /tmp/current.zip
echo "Done."
