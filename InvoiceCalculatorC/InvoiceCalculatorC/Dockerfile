FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR invoicecalculatorc

EXPOSE 80
EXPOSE 5024

#Copy proyect files
COPY ./*.csproj ./
RUN dotnet restore

#Copy eveihing else

COPY . .
RUN dotnet publish -c Release -o out

#Build image
FROM mcr.microsoft.com/dotnet/sdk:6.0
WORKDIR /invoicecalculatorc
COPY --from=build /invoicecalculatorc/out .
ENTRYPOINT ["dotnet", "InvoiceCalculatorC.dll"]
