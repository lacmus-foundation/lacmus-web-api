FROM mcr.microsoft.com/dotnet/core/sdk:3.1-buster
LABEL author="gosha20777"

ENV DOTNET_USE_POLLING_FILE_WATCHER=1
ENV ASPNETCORE_URLS=http://*:5000

EXPOSE 5000

WORKDIR /var/www/Identity
COPY . .

CMD ["/bin/bash", "-c", "dotnet restore && dotnet watch run"]