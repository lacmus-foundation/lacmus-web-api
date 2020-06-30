# Microsoft has a new "Hub" location for images that 
# can be used for ASP.NET Core 2+
# FROM mcr.microsoft.com/dotnet/core/sdk:2.2

FROM microsoft/dotnet:3.1-sdk

LABEL author="gosha20777"

ENV DOTNET_USE_POLLING_FILE_WATCHER=1
ENV ASPNETCORE_URLS=http://*:5000

EXPOSE 5000

WORKDIR /var/www/apiIdentity

CMD ["/bin/bash", "-c", "dotnet restore && dotnet watch run"]