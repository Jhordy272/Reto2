package com.uniandes.InvoiceCalculatorJava.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class InvoiceRequest {

    private List<InvoiceItemRequest> items;
}
