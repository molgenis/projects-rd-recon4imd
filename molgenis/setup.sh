#!/bin/sh
emx2_host=''
user_email=''
user_password=''
primary_schema=''

# ////////////////////////////////////////////////////////////////////////////

# Create functions that generate new GraphQL queries
new_signin_query () {
    local email=$1
    local password=$2
    query='mutation {
        signin (email: "'$email'", password: "'$password'") {
            status
            message
            token
        }
    }'
    echo $query
}

new_create_schema_query () {
    local name=$1
    local description=$2
    query='mutation {
        createSchema (name: "'$name'", description: "'$description'") {
            status
            message
        }
    }'
    echo $query
}

new_update_schema_query () {
    local name=$1
    local description=$2
    query='mutation {
        updateSchema (name: "'$name'", description: "'$description'") {
            status
            message
        }
    }'
    echo $query
}

new_delete_schema_query () {
    local id=$1
    query='mutation {
        deleteSchema (id: "'$id'") {
            status
            message
        }
    }'
    echo $query
}

new_change_members_query () {
    local email=$1
    local role=$2
    query='mutation {
        change (members: [{email:"'$email'", role:"'$role'"}]) {
            status
            message
        }
    }'
    echo $query
}

new_change_setting_query () {
    local setting=$1
    local value=$2
    query='mutation {
        change (settings:[{key: "'$setting'", value: '$value'}]) {
            status
            message
        }
    }'
    echo $query
}

new_save_query () {
  local table=$1
  local data=$2
  query='mutation {
    save ('$table': '$data') {
      status
      message
    }
  }'
  echo $query
}

new_update_query () {
  local table=$1
  local data=$2
  query='mutation {
    update ('$table': '$data') {
      status
      message
    }
  }'
  echo $query
}

random_key () {
  local length=${1:-12}
  echo "$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w $length | head -n 1 )"
}

# ////////////////////////////////////////////////////////////////////////////

# sign in and get token
signin_gql=$(new_signin_query $user_email $user_password)
api_token=$(curl "${emx2_host}/api/graphql" \
    -H "Content-Type: application/json" \
    -d "$(jq -c -n --arg query "$signin_gql" '{"query": $query}')" \
    | grep "token" | tr -d '"' | awk '{print $3}'
)

echo $api_token

#~~~~~~~~~~~~~~
# ~ OPTIONAL ~
# remove existing schemas
declare -a schemas_to_remove=(
  "catalogue-demo"
  "CatalogueOntologies"
  "pet store"
)

for schema in "${schemas_to_remove[@]}"
do
    delete_schema_gql=$(new_delete_schema_query $schema)
    curl -s "${emx2_host}/api/graphql" \
        -H "Content-Type: application/json" \
        -H "x-molgenis-token:${api_token}" \
        -d "$(jq -c -n --arg query "$delete_schema_gql" '{"query": $query}')"
done

# //////////////////////////////////////

# init primary schema - load menu, change membership, add description

public_menu=$(jq '.menu | map(. + {key: "'$(random_key 7)'"}) | tostring' molgenis/schema_menu.json)
set_menu_gql=$(new_change_setting_query "menu" $public_menu)
menu_payload="$(jq -c -n --arg query "$set_menu_gql" '{"query": $query}')"
echo $menu_payload

set_menu_response=$(curl -s "${emx2_host}/${primary_schema}/api/graphql" \
    -H "Content-Type: application/json" \
    -H "x-molgenis-token:${api_token}" \
    -d $menu_payload)

set_menu_status=(jq '.data.createSchema.status' <<< $set_menu_response | xargs)
if [ $set_menu_status == "SUCCES" ]
then
  echo "Updated menu: $set_menu_response"
fi