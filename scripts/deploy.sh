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
    esac
done

if [[ -z $update_secrets ]]; then
    echo "Error: Include parameters for update_secrets for cloudformation template"
fi

SecretsName=sahil-test-4-process-bp-project-"secrets"

if [[ "$update_secrets" == "true" ]]; then
    bash scripts/addSecrets.sh
fi


sam.exe build --parameter-overrides SecretsName=$SecretsName
sam.exe deploy --guided --parameter-overrides SecretsName=$SecretsName