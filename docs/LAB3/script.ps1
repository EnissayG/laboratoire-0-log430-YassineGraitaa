# Dossiers
$input = "."
$output = ".\output_images"

New-Item -ItemType Directory -Path $output -Force

Get-ChildItem -Path $input -Filter *.puml -Recurse | ForEach-Object {
   java -jar plantuml.jar -tpng -o $output $_.FullName
}
