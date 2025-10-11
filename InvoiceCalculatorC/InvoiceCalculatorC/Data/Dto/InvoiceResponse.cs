using InvoiceCalculatorC.Models;

namespace InvoiceCalculatorC.Data.Dto;

public class InvoiceResponse
{
    public List<Product> items { get; set; }
    public double total { get; set; }

    public InvoiceResponse(List<Product> items, double total)
    {
        this.items = items;
        this.total = total;
    }
}