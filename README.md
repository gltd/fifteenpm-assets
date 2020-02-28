fifteenpm-assets
================

Assets for [fifteen.pm](https://fifteen.pm) releases and promotion. We keep record of this repo for utilities and documentation, but all assets are stored on S3.

 You can download assets locally by setting up `awscli`, adding a `gltd` profile, and running `make upload_assets` to sync your local assets to S3, and `make download_assets` to remote changes from s3. 
 
It's best to follow these conventions:

* When you want to add new assets
  - Add your files in the [assets](assets/) directory.
  - Follow the present folder structure and naming convention:
    - `15pm-{release_number}-{track_name}-{asset_description}-{author}.{filetype}`
    - EG: `15pm-9-cityLife-loop-ba.mp4`
  - Make a commit 
  - Push to master
  - Run `make upload_assets`
    - This will also take a snapshot of the current `assets` directory and save it on s3 under the associated commit's SHA.
* When you want to get new assets:
  - Check if there are changes on master.
  - Pull
  - Run `make download_assets`
    - This will allow you to determine how to handle overwrite behavior.
    - If you want to clear your local assets, just run `rm --rf assets` and then run `make download_assets` again.