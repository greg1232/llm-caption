# e exit on first failure
# x all executed commands are printed to the terminal
# u unset variables are errors
# a export all variables to the environment
# E any trap on ERR is inherited by shell functions
# -o pipefail | produces a failure code if any stage fails
set -Eeuoxa pipefail

# Get the directory of this script
LOCAL_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Run the docker container
docker run --rm -it --user $(id -u):$(id -g) \
    --volume "$LOCAL_DIRECTORY:/app/cmd" \
    --volume "$LOCAL_DIRECTORY/../scripts:/app/scripts" \
    --volume "$LOCAL_DIRECTORY/bashly-settings.yml:/app/bashly-settings.yml" \
    dannyben/bashly "$@"

