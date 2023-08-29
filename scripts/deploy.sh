usage() {
    echo "Usage: $0 --update_secrets <true | false>"
    exit 1
}

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --update_secrets)
            update_secrets="$2"
            shift
            shift
            ;;
        --stage)
            stage="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown argument: $key"
            usage
            ;;
    esac
done

# Get the directory containing the script
script_dir=$(dirname "$(realpath "$0")")
bash $script_dir/createAllUtilsSymlink.sh

if [[ -z $update_secrets ]]; then
    echo "Error: Include parameters for update_secrets for cloudformation template"
fi

if [[ -z $AWS_DEFAULT_REGION ]]; then
    echo "Warning: AWS_DEFAULT_REGION not found, using a default of us-east-1"
    export AWS_DEFAULT_REGION="us-east-1"
fi

SecretsName="sahil-check-functions-process-bp-project-$stage-secrets"
StackName="sahil-check-functions-process-bp-project-$stage"
BucketName="sahil-check-functions-process-bp-project-$stage-bucket"

if ! aws s3api head-bucket --bucket $BucketName 2>/dev/null; then
          aws s3api create-bucket --bucket $BucketName
          fi


if [[ "$update_secrets" == "true" ]]; then
    bash scripts/addSecrets.sh $stage
fi


sam build --parameter-overrides SecretsName=$SecretsName
sam deploy --stack-name $StackName \
    --s3-bucket $BucketName \
    --parameter-overrides SecretsName=$SecretsName \
    --s3-prefix "check-functions" \
    --capabilities CAPABILITY_IAM