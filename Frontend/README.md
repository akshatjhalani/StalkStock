# Stalk Stock Frontend: Angular Application#

### Top-level directory layout

    .
    ├── dist                   # Compiled files (alternatively `dist`)
    ├── src                    # Source files (alternatively `app`)
			app
			└── dashboard
				├── home
				│   └── detail
				├── subscription
				│  
				└── layout
					└── top-nav
			└── login
			└── model
				├── stock
			└── service
				├── dashboard
				├── subscription
				├── user
			└── shared
				├── notification-service
				├── toaster-service
			assets
			└──	images
			
    └── README.md

### Steps to deploy locally

Build the image using the following command

```bash
$ docker build -t stock:latest .
```

Run the Docker container using the command shown below.

```bash
$ docker run -d -p 4200:4000 stock
```

The Application UI will be accessible at https://<host_ip>:4200`


### Steps to deploy on Aws S3
1. Upload files in dist folder to S3 public bucket
2. Enable Static web hosting for the bucket and set public access
3. Use the bucket public URL to access website
