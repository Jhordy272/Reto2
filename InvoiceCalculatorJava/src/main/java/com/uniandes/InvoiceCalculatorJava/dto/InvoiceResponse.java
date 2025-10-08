package com.uniandes.InvoiceCalculatorJava.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class InvoiceResponse {

    private List<InvoiceItemResponse> items;
    private Double total;
}
