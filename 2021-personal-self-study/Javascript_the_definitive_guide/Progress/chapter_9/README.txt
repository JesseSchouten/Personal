To recreate the directory:

package.json (add to scripts -> "build:package": "npm install && npm install csvtojson"):
npm init 

tsconfig.json (adjust parameters):
tsc --init

npm run build:package

If tsconfig was adjusted as in this directory, compile the files using:
tsc


