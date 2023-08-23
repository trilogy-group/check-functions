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
        *)
            echo "Unknown argument: $key"
            usage
    esac
done

if [[ -z $update_secrets ]]; then
    echo "Error: Include parameters for update_secrets for cloudformation template"
fi

SecretsName=sahil-test-4-process-bp-project-"secrets"

if [[ "$update_secrets" == "true" ]]; then
    bash scripts/addSecrets.sh
fi


sam build --parameter-overrides SecretsName=$SecretsName
sam deploy --guided --parameter-overrides SecretsName=$SecretsName