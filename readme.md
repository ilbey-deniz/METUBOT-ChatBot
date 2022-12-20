# Sunucu ayağa kaldırma
## Bağlanma
```
ssh metubot@metubot.ceng.metu.edu.tr -p 8085
sudo su
```
Sunucuya giriş yaptıktan sonra root kullanıcısına geçilmelidir çünkü işlemler orda çalıştırılıyor (node.js, python vs.).

## Sunucu: Nginx
`sudo systemctl restart nginx`

## İşlem yönetimi
İşlemleri yönetmek için pm2 var. Takip ettiğim [sunucu rehberi](https://hackernoon.com/a-tutorial-to-deploy-the-nodejs-app-to-nginx-server) bunu indirtti bana.
İşlem başlatma: `pm2 start dosya`
İşlem listesi: `pm2 ls`
İşlem logları: `pm2 logs`
İşlem durdurma: `pm2 stop id`
### Çalıştırılacak işlemler
#### Node.js
```
cd web/backend
npm install
pm2 start node.js
```
#### Python
```
pm2 start index.py
```
# Sunucuda Değişiklik Yapma
## Sunucu: Nginx
Sunucuya istek gelince ufw güvenlik duvarından geçerek nginx'e gelir, oradan reverse proxy ile web/backend/node.js'e aktarılır. Node.js python ile iletişime geçer, sonucu geri istemciye yollar.
Nginx baştan başlatma komutu:
`sudo systemctl restart nginx`
Sunucu dosyası konumu:
`/etc/nginx/sites-available/metubot.ceng.metu.edu.tr`
## Kaynak kodu güncelleme
`git pull` yapılarak proje güncellenir. Derlenmeye gerek olmayan kodlar alınmış olur.
### Frontend
frontend kodu güncellenince `npm run build` denilerek production için derlenir, derlenen kod commit ve push yapılır, suncuuda git pull yapılıp derlenen kod alınır. 
