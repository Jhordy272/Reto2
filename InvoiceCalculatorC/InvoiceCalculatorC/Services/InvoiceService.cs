using InvoiceCalculatorC.Data;
using InvoiceCalculatorC.Data.Dto;
using InvoiceCalculatorC.Models;

namespace InvoiceCalculatorC.Services;

public class InvoiceService
{
    public static InvoiceResponse calculateInvoice(InvoiceRequest request, ProductsDb pdb)
    {
        double total = 0;
        List<Product> totalProducts = new List<Product>();
        bool isFailCalc = isFailedCalc();
        foreach (var product in request.items)
        {
            Product productDb = pdb.Products.FindAsync(product.productId).Result;
            if (productDb != null)
            {
                if (productDb.stock >= product.quantity)
                {
                    totalProducts.Add(productDb);
                    if (isFailCalc)
                    {
                        total += productDb.price * -1;  
                    }
                    else
                    {
                        total += productDb.price * product.quantity;  
                    }
                }
            }
        }
        return new InvoiceResponse(totalProducts, total);
    }

    private static bool isFailedCalc()
    {
        Random random = new Random();
        int randomNumer = random.Next(1, 11);
        if (randomNumer == 10)
        {
            return true;
        }
        return false;
    } 
    
}