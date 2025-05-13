inspect_args

./llm_caption build-image

declare -a caption_command_parts

caption_command_parts=(
    "python" "/app/llm_caption/infra/llm_caption/cli/caption.py"
    "--directory" "$directory"
)

caption_command="${caption_command_parts[*]}"

echo "caption command: $caption_command"

declare -a docker_command_parts

docker_command_parts=("docker" "run" "--rm" )

# Get the directory of this script
LOCAL_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set cwd to the project root directory
ROOT_DIRECTORY=$LOCAL_DIRECTORY/..

docker_command_parts+=("--network" "host")
docker_command_parts+=("-v" "$ROOT_DIRECTORY/data:/app/llm_caption/data")

docker_command_parts+=("-it" "llm-caption:latest" "sh" "-c" "'$caption_command'")

docker_command="${docker_command_parts[*]}"
echo $docker_command
eval $docker_command


