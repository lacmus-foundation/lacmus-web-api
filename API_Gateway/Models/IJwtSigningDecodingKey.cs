using Microsoft.IdentityModel.Tokens;

namespace API_Gateway.Models
{
    public interface IJwtSigningDecodingKey
    {
        SecurityKey GetKey();
    }
}