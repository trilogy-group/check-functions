# MyProject  

# Getting Started

It is recommended to use Devspaces for development with this template as it uses `gitpod.yml` file for an automatic setup.
1. Open a Devspaces workspace for the generated repo.
2. Copy the Private RSA Key for the service from your project's details page.
3. Enter the RSA key in Devspaces terminal and then hit enter twice.
4. Fill the values corresponding to the [required environment variables](env/.env.dev.template).
5. Your application will now be up and running. 

## Structure
The checks are present in the `/src/checks/{check_name}.` folder. Some common utilities are present in the `/src/checks/{check_name}/utils` folder. Unit tests are present in the `/src/checks/{check_name}/tests` folder.

## Prompt Testing
The prompts can be tested using promptfoo. These instructions for running these tests can be found under `/src/checks/{check_name}/tests/promptfoo/README.md`

## Deploying
To deploy the check functions,
1. Make sure you have logged in with `saml2aws`.
2. Run `export AWS_DEFAULT_REGION={name-of-region}`.
3. Set the name of the secrets, stack and bucket to be used over [here](scripts/deploy.sh#L35)
<!-- Ideally, this name will be generated using the name of the project and service when creating a template. -->
4. Run `bash scripts/deploy.sh --update_secrets <true/false> --stage <dev/prod>`. The update_secrets parameter should be set to `true` if deploying for the first time, or if the values in the `.env` have been updated. The `stage` should be set to either dev or prod.
