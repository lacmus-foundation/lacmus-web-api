using Microsoft.IdentityModel.Tokens;

namespace API_Gateway.Models
{
    public interface IJwtSigningEncodingKey
    {
        string SigningAlgorithm { get; }
 
        SecurityKey GetKey();
    }
}