using InvoiceCalculatorC.Data;
using InvoiceCalculatorC.Data.Dto;
using InvoiceCalculatorC.Models;
using InvoiceCalculatorC.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Obtener variables de entorno
var host = Environment.GetEnvironmentVariable("DB_HOST") ?? "localhost";
var port = Environment.GetEnvironmentVariable("DB_PORT") ?? "5432";
var dbName = Environment.GetEnvironmentVariable("DB_NAME") ?? "inventary";
var user = Environment.GetEnvironmentVariable("DB_USER") ?? "postgres";
var password = Environment.GetEnvironmentVariable("DB_PASSWORD") ?? "password";

// Construir la cadena de conexión
var connectionString = $"Host={host};Port={port};Database={dbName};Username={user};Password={password};";

builder.Services.AddDbContext<ProductsDb>(options => options.UseNpgsql(connectionString));

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();


app.MapPost("/product/", async (Product pr, ProductsDb pdb) =>
{
    pdb.Products.Add(pr);
    await pdb.SaveChangesAsync();
    
    return Results.Created($"/products/{pr.id}", pr);
});

app.MapGet("/products/{id:long}", async (long id, ProductsDb pdb) =>
{
    return await pdb.Products.FindAsync(id)
        is Product p ? Results.Ok(p) : Results.NotFound();
});

app.MapPost("/invoice/calculate/", (InvoiceRequest request, ProductsDb pdb) =>
{
    InvoiceResponse totalCalculation = InvoiceService.calculateInvoice(request, pdb);
    if (totalCalculation.items.Count() > 0)
    {
        return Results.Ok(totalCalculation);
    }
    return Results.NotFound();
});

app.Run();

record WeatherForecast(DateTime Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}