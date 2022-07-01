# URL Shortener

[![codecov](https://codecov.io/gh/allanjuliani/shortener/branch/main/graph/badge.svg?token=z6xvRrXL5n)](https://codecov.io/gh/allanjuliani/shortener)

## 🐋 Using Docker

### Install Docker

https://docs.docker.com/engine/install/

https://docs.docker.com/compose/install/

### 🖥️ Install project
```commandline
make install
```

### 🧪 Run tests
```commandline
make tests
```

### 🔍 Show coverage
```commandline
make cov
```

### 👤 Create superuser for admin
This command will create a user based on environment var defined at .env file
```commandline
make createsuperuser
```

#### Admin URL to access on browser
http://localhost/admin/
