using Microsoft.IdentityModel.Tokens;

namespace API_Gateway.Models
{
    public interface IJwtEncryptingDecodingKey
    {
        SecurityKey GetKey();
    }
}