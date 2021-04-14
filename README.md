# lambda coffee counter

zip project code then to provision:
```
cd coffeescript/infra
terraform init
terraform plan -out=coffeecounter.out
terraform apply coffeecounter.out
```
