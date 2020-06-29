using Microsoft.IdentityModel.Tokens;

namespace API_Gateway.Models
{
    public interface IJwtEncryptingEncodingKey
    {
        string SigningAlgorithm { get; }
 
        string EncryptingAlgorithm { get; }
 
        SecurityKey GetKey();
    }
}