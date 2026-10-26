# hub-vinitech

My hub site

## Publicação e deploy

O workflow `Publish image` publica no GHCR privado usando o `GITHUB_TOKEN` do
próprio repositório. Builds da branch `main` produzem as tags do SHA do commit e
`main`, para Linux amd64 e arm64. A execução é serializada para impedir que um
build antigo sobrescreva o canal depois de um build mais novo.

Manifestos de produção, versão da imagem e configuração de deploy ficam no
repositório privado [vps-infra](https://github.com/ViniciusRossmann/vps-infra), em
`apps/hub-vinitech`. O Image Updater registra o digest no Git e o Argo CD Core
reconcilia o k3s. O pipeline termina na publicação; o estado do deploy é consultado
no Argo/Kubernetes.

O workflow não acessa a VPS por SSH e não precisa de kubeconfig nem secrets de
deploy. Não reexecute workflows antigos de deploy por SSH. As etapas de adoção,
ativação de imagens e rollback estão documentadas no repositório central.
