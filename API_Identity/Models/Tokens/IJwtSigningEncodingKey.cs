using Microsoft.IdentityModel.Tokens;

namespace API_Identity.Models.Tokens
{
    public interface IJwtSigningEncodingKey
    {
        string SigningAlgorithm { get; }
 
        SecurityKey GetKey();
    }
}