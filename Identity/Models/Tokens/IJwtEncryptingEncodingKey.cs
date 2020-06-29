using Microsoft.IdentityModel.Tokens;

namespace Identity.Models.Tokens
{
    public interface IJwtEncryptingEncodingKey
    {
        string SigningAlgorithm { get; }
 
        string EncryptingAlgorithm { get; }
 
        SecurityKey GetKey();
    }
}