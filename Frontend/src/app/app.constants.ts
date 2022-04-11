import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
/**
 * Global constants file
 */
export class ApiConstants {
    public BaseUrl = "https://evnincj8c8.execute-api.us-east-1.amazonaws.com/prod/sas/"
    public PriceUrl = "https://310nr5j5qe.execute-api.us-east-1.amazonaws.com/" //"http://localhost:4200/price/"
    public SubscriptionUrl = "https://ygeown8ckk.execute-api.us-east-1.amazonaws.com/stocksent1/"//"http://localhost:4200/subscription/"
}
