using Microsoft.IdentityModel.Tokens;

namespace Identity.Models.Tokens
{
    public interface IJwtSigningEncodingKey
    {
        string SigningAlgorithm { get; }
 
        SecurityKey GetKey();
    }
}